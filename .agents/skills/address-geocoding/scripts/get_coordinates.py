import sys
import os
import json
import re
import argparse
import urllib.request
import urllib.parse
from pathlib import Path

# geopy for fallback
try:
    from geopy.geocoders import Nominatim
    from geopy.exc import GeocoderTimedOut, GeocoderServiceError
    HAS_GEOPY = True
except ImportError:
    HAS_GEOPY = False

# Windows 콘솔 등에서의 UTF-8 출력 지원
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')


def load_env_file():
    """
    현재 작업 디렉터리, 스크립트 위치, 스킬 루트 디렉터리의 .env 파일을 탐색하여 환경 변수에 로드합니다.
    """
    script_dir = Path(__file__).resolve().parent
    skill_dir = script_dir.parent
    workspace_dir = skill_dir.parent.parent if skill_dir.parent.name == "skills" else Path.cwd()

    candidates = [
        skill_dir / ".env",
        workspace_dir / ".env",
        Path.cwd() / ".env",
        script_dir / ".env",
    ]

    for env_path in candidates:
        if env_path.exists() and env_path.is_file():
            try:
                with open(env_path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if not line or line.startswith("#") or "=" not in line:
                            continue
                        key, val = line.split("=", 1)
                        key = key.strip()
                        val = val.strip().strip("'\"")
                        if key and val and key not in os.environ:
                            os.environ[key] = val
            except Exception:
                pass


def clean_address_query(query: str) -> str:
    """
    상세 주소(층, 호수, 부가 상호 등)를 정제하여 도로명/지번 검색 성공률을 높입니다.
    예: '부산 남구 남동천로 128 BIFC2 스퀘어가든 2층 코스모스' -> '부산 남구 남동천로 128'
    """
    # 1. 층수/호수 패턴 제거
    cleaned = re.sub(r'(\b\d+층\b|\b\d+호\b|\b\d+호실\b|\b지하\s*\d+층\b)', '', query)
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    return cleaned


def geocode_vworld_address(query: str, api_key: str, domain: str = "http://localhost", addr_type: str = "road"):
    """
    VWorld Geocoder 2.0 API를 호출하여 도로명 또는 지번 주소를 좌표로 변환합니다.
    URL 예시:
    https://api.vworld.kr/req/address?service=address&request=getcoord&version=2.0&crs=epsg:4326&address={query}&refine=true&simple=false&format=json&type={addr_type}&key={api_key}
    """
    url = "https://api.vworld.kr/req/address"
    params = {
        "service": "address",
        "request": "getcoord",
        "version": "2.0",
        "crs": "epsg:4326",
        "address": query,
        "refine": "true",
        "simple": "false",
        "format": "json",
        "type": addr_type.lower(),
        "key": api_key,
    }
    if domain:
        params["domain"] = domain

    encoded_params = urllib.parse.urlencode(params)
    req_url = f"{url}?{encoded_params}"

    req = urllib.request.Request(
        req_url,
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"}
    )
    with urllib.request.urlopen(req, timeout=10) as response:
        if response.status == 200:
            data = json.loads(response.read().decode('utf-8'))
            resp = data.get("response", {})
            status = resp.get("status")

            if status == "OK" and "result" in resp:
                point = resp["result"]["point"]
                refined = resp.get("refined", {})
                structure = refined.get("structure", {})
                road_name = structure.get("level4L", "")
                detail = structure.get("detail", "")
                level5 = structure.get("level5", "")

                road_address_parts = [structure.get("level1"), structure.get("level2"), road_name, level5]
                road_address = " ".join([p for p in road_address_parts if p]).strip()

                return {
                    "success": True,
                    "source": "vworld_geocoder",
                    "query": query,
                    "address": refined.get("text", query),
                    "road_address": road_address or refined.get("text", ""),
                    "parcel_address": structure.get("level4A", ""),
                    "latitude": float(point["y"]),
                    "longitude": float(point["x"]),
                    "raw": data
                }
            elif status == "ERROR":
                err = resp.get("error", {})
                # 인증키 오류 또는 권한 오류가 있을 경우 로깅
                return {
                    "success": False,
                    "source": "vworld_error",
                    "error_code": err.get("code"),
                    "message": err.get("text", "VWorld API 인증 또는 요청 오류")
                }
    return None


def search_vworld_place(query: str, api_key: str, domain: str = "http://localhost"):
    """
    VWorld 검색 2.0 API를 호출하여 장소/건물명(POI)을 좌표로 변환합니다.
    """
    url = "https://api.vworld.kr/req/search"
    params = {
        "service": "search",
        "request": "search",
        "version": "2.0",
        "crs": "EPSG:4326",
        "size": "5",
        "page": "1",
        "query": query,
        "type": "place",
        "format": "json",
        "key": api_key,
    }
    if domain:
        params["domain"] = domain

    encoded_params = urllib.parse.urlencode(params)
    req_url = f"{url}?{encoded_params}"

    req = urllib.request.Request(
        req_url,
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"}
    )
    with urllib.request.urlopen(req, timeout=10) as response:
        if response.status == 200:
            data = json.loads(response.read().decode('utf-8'))
            resp = data.get("response", {})
            if resp.get("status") == "OK" and "result" in resp:
                items = resp["result"].get("items", [])
                if items:
                    first = items[0]
                    point = first.get("point", {})
                    addr_info = first.get("address", {})
                    return {
                        "success": True,
                        "source": "vworld_search",
                        "query": query,
                        "title": first.get("title", ""),
                        "address": addr_info.get("road") or addr_info.get("parcel") or first.get("title", ""),
                        "road_address": addr_info.get("road", ""),
                        "parcel_address": addr_info.get("parcel", ""),
                        "latitude": float(point["y"]),
                        "longitude": float(point["x"]),
                        "raw": data
                    }
    return None


def geocode_vworld(query: str, api_key: str, domain: str = "http://localhost"):
    """
    VWorld API (도로명 주소 -> 지번 주소 -> 정제 주소 -> 장소 검색) 순서로 좌표를 조회합니다.
    """
    # 1. 도로명 주소(road) 검색 시도
    res = geocode_vworld_address(query, api_key, domain, addr_type="road")
    if res and res.get("success"):
        return res
    if res and res.get("source") == "vworld_error":
        # 인증 오류인 경우 즉시 에러 반환하여 알림
        return res

    # 2. 지번 주소(parcel) 검색 시도
    res = geocode_vworld_address(query, api_key, domain, addr_type="parcel")
    if res and res.get("success"):
        return res

    # 3. 층수/호수 정제 후 도로명/지번 재시도
    cleaned = clean_address_query(query)
    if cleaned != query:
        res = geocode_vworld_address(cleaned, api_key, domain, addr_type="road")
        if res and res.get("success"):
            res["query"] = query
            return res
        res = geocode_vworld_address(cleaned, api_key, domain, addr_type="parcel")
        if res and res.get("success"):
            res["query"] = query
            return res

    # 4. 장소/POI 키워드 검색 시도
    res = search_vworld_place(query, api_key, domain)
    if res and res.get("success"):
        return res

    if cleaned != query:
        res = search_vworld_place(cleaned, api_key, domain)
        if res and res.get("success"):
            res["query"] = query
            return res

    return None


def geocode_nominatim(query: str):
    """
    Nominatim (OpenStreetMap) 백업 지오코딩
    """
    if not HAS_GEOPY:
        return {
            "success": False,
            "query": query,
            "message": "geopy 패키지가 설치되어 있지 않아 폴백 조회를 수행할 수 없습니다."
        }

    geolocator = Nominatim(user_agent="address_geocoding_skill")
    try:
        location = geolocator.geocode(query, timeout=10)
        if not location:
            cleaned = clean_address_query(query)
            if cleaned != query:
                location = geolocator.geocode(cleaned, timeout=10)

        if not location:
            return {
                "success": False,
                "query": query,
                "message": f"'{query}'에 대한 위치 정보를 찾을 수 없습니다. 도로명/지번/장소명을 확인해 주세요."
            }

        raw_data = location.raw
        return {
            "success": True,
            "source": "nominatim_osm",
            "query": query,
            "address": location.address,
            "latitude": location.latitude,
            "longitude": location.longitude,
            "place_id": raw_data.get("place_id"),
            "osm_type": raw_data.get("osm_type"),
            "category": raw_data.get("class"),
            "type": raw_data.get("type"),
            "boundingbox": raw_data.get("boundingbox")
        }
    except GeocoderTimedOut:
        return {"success": False, "query": query, "message": "지오코딩 서비스 요청 시간 초과"}
    except GeocoderServiceError as e:
        return {"success": False, "query": query, "message": f"지오코딩 서비스 오류: {e}"}
    except Exception as e:
        return {"success": False, "query": query, "message": f"오류 발생: {e}"}


def geocode_address(query: str, api_key: str = None, domain: str = "http://localhost", as_json: bool = False):
    """
    주소 또는 장소명을 입력받아 위경도 및 상세 위치 정보를 조회합니다.
    VWorld API 키가 유효하면 VWorld를 사용하고, 없거나 실패 시 Nominatim을 사용합니다.
    """
    load_env_file()

    key = api_key or os.environ.get("VWORLD_API_KEY", "").strip()
    domain = domain or os.environ.get("VWORLD_DOMAIN", "http://localhost").strip()

    result = None

    if key:
        try:
            result = geocode_vworld(query, key, domain)
        except Exception:
            result = None

    # VWorld 결과가 없거나 실패 시 Nominatim으로 폴백
    if not result or not result.get("success"):
        vworld_err = result.get("message") if result and result.get("source") == "vworld_error" else None
        nominatim_result = geocode_nominatim(query)
        if nominatim_result.get("success"):
            result = nominatim_result
            if vworld_err:
                result["vworld_warning"] = f"VWorld 오류({vworld_err})로 인해 OpenStreetMap으로 대체 조회되었습니다."
        elif result is None:
            result = nominatim_result

    if as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        if result and result.get("success"):
            source_label = "VWorld (국토교통부 공간정보)" if "vworld" in result.get("source", "") else "OpenStreetMap (Nominatim)"
            print("========================================")
            print(f"주소 및 위경도(좌표) 변환 결과 [{source_label}]")
            print("========================================")
            print(f"- 검색어       : {query}")
            if result.get("title"):
                print(f"- 명칭(장소명) : {result.get('title')}")
            print(f"- 전체 주소    : {result.get('address')}")
            if result.get("road_address"):
                print(f"- 도로명 주소  : {result.get('road_address')}")
            if result.get("parcel_address"):
                print(f"- 지번 주소    : {result.get('parcel_address')}")
            print(f"- 위도(Lat)    : {result.get('latitude')}")
            print(f"- 경도(Lon)    : {result.get('longitude')}")
            print(f"- 데이터 출처  : {source_label}")
            if result.get("vworld_warning"):
                print(f"- 안내         : {result.get('vworld_warning')}")
            print("========================================")
        else:
            print(f"[검색 실패] {result.get('message', '위치 정보를 찾을 수 없습니다.') if result else '위치 정보를 찾을 수 없습니다.'}")


def main():
    parser = argparse.ArgumentParser(description="VWorld 및 OpenStreetMap 기반 주소/장소명 위경도 좌표 변환기")
    parser.add_argument("query", nargs="+", help="조회할 주소 또는 장소명 (예: '효령로72길 60', '부산 남구 문현금융로 40')")
    parser.add_argument("--key", "-k", help="VWorld API 인증키 (생략 시 VWORLD_API_KEY 환경변수 또는 .env 파일 사용)")
    parser.add_argument("--domain", "-d", default="http://localhost", help="VWorld 인증키 발급 시 등록한 서비스 URL/도메인 (기본값: http://localhost)")
    parser.add_argument("--json", action="store_true", help="결과를 JSON 형식으로 출력합니다.")

    args = parser.parse_args()
    query_str = " ".join(args.query)

    geocode_address(query_str, api_key=args.key, domain=args.domain, as_json=args.json)


if __name__ == "__main__":
    main()
