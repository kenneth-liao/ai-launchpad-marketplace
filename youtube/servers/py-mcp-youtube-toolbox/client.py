import asyncio
import sys
import json
import logging
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from typing import Any, Dict, List, Optional

# --- 로깅 설정 ---
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 서버 스크립트 파일명 (실제 서버 파일명과 일치해야 함)
SERVER_SCRIPT_FILENAME = "server.py"

async def run_tool_call(tool_name: str, arguments: Dict[str, Any]) -> None:
    """지정된 Tool 이름과 파라미터로 MCP 서버의 Tool을 호출하고 결과를 출력합니다."""

    # 서버 실행 설정: 현재 디렉토리의 SERVER_SCRIPT_FILENAME을 python으로 실행
    server_params = StdioServerParameters(
        command=sys.executable, # 현재 사용 중인 파이썬 인터프리터 사용
        args=[SERVER_SCRIPT_FILENAME],
        env=None, # 필요시 환경 변수 전달 가능
    )

    print(f"--- YouTube MCP 서버 호출 요청 ---")
    print(f"   이름: {tool_name}")
    print(f"   Arguments: {json.dumps(arguments, indent=2, ensure_ascii=False)}") # 인자 예쁘게 출력

    try:
        # stdio_client를 사용하여 서버 프로세스 시작 및 연결
        async with stdio_client(server_params) as (read, write):
            # ClientSession 생성
            async with ClientSession(read, write) as session:
                # 서버와 초기 핸드셰이크 수행
                await session.initialize()
                logger.info("YouTube MCP 서버와 연결 초기화 완료.")

                # (선택 사항) 사용 가능한 리소스 및 툴 목록 확인
                try:
                    # 사용 가능한 리소스 확인
                    resources_info = await session.list_resources()
                    available_resources = [resource.name for resource in resources_info.resources] if hasattr(resources_info, 'resources') else []
                    available_resource_uris = [resource.uri for resource in resources_info.resources] if hasattr(resources_info, 'resources') else []
                    logger.info(f"서버에서 사용 가능한 Resources: {available_resources}")
                    logger.info(f"서버에서 사용 가능한 Resource URIs: {available_resource_uris}")

                    # 사용 가능한 툴 목록 확인
                    tools_info = await session.list_tools()
                    available_tools = [tool.name for tool in tools_info.tools] if hasattr(tools_info, 'tools') else []
                    logger.info(f"서버에서 사용 가능한 Tools: {available_tools}")

                    # 사용 가능한 프롬프트 확인
                    prompts_info = await session.list_prompts()
                    available_prompts = [prompt.name for prompt in prompts_info.prompts] if hasattr(prompts_info, 'prompts') else []
                    logger.info(f"서버에서 사용 가능한 Prompts: {available_prompts}")

                    # 지정된 이름이 어떤 타입인지 확인
                    is_tool = tool_name in available_tools
                    is_prompt = tool_name in available_prompts
                    is_resource = tool_name in available_resources
                    is_resource_uri = tool_name.startswith("youtube://")
                    
                    # 아무데도 없으면 경고
                    if not (is_tool or is_prompt or is_resource or is_resource_uri):
                        logger.warning(f"경고: 요청된 '{tool_name}'이 서버의 사용 가능 목록에 없습니다. 호출을 시도합니다.")

                except Exception as e:
                    logger.warning(f"사용 가능한 리소스/Tool/Prompt 목록 조회 중 오류 발생: {e}")
                    is_tool = True  # 기본적으로 tool로 시도
                    is_prompt = False
                    is_resource = False
                    is_resource_uri = tool_name.startswith("youtube://")

                # 결과 변수 초기화
                result = None

                # Tool 또는 Resource 호출
                if is_resource_uri:
                    # Resource URI 직접 호출
                    logger.info(f"'{tool_name}' Resource URI 호출 중...")
                    result = await session.fetch_resource(tool_name, query_params=arguments)
                elif is_tool:
                    # Tool 호출
                    logger.info(f"'{tool_name}' Tool 호출 중...")
                    result = await session.call_tool(tool_name, arguments=arguments)
                elif is_prompt:
                    # Prompt 호출
                    logger.info(f"'{tool_name}' Prompt 호출 중...")
                    result = await session.call_prompt(tool_name, arguments=arguments)
                else:
                    # 이름으로 Resource 호출 시도
                    logger.info(f"'{tool_name}' Resource 이름으로 호출 시도 중...")
                    try:
                        # 이름에 맞는 리소스 URI 찾기
                        matching_resource = next((r for r in resources_info.resources if r.name == tool_name), None)
                        if matching_resource:
                            result = await session.fetch_resource(matching_resource.uri, query_params=arguments)
                        else:
                            # 마지막 수단으로 툴 호출 시도
                            result = await session.call_tool(tool_name, arguments=arguments)
                    except Exception as resource_error:
                        logger.error(f"Resource 호출 실패, tool로 시도: {resource_error}")
                        result = await session.call_tool(tool_name, arguments=arguments)

                logger.debug(f"호출 원시 결과: {result}") # 디버깅 시 상세 결과 확인

                # 결과 출력
                print("\n--- 호출 결과 ---")
                if hasattr(result, 'content') and result.content:
                    # 결과 내용이 여러 개일 수 있으므로 반복 처리
                    for content_item in result.content:
                        if hasattr(content_item, 'text'):
                            # JSON 형식의 텍스트일 경우 파싱하여 예쁘게 출력 시도
                            try:
                                parsed_json = json.loads(content_item.text)
                                print(json.dumps(parsed_json, indent=2, ensure_ascii=False))
                            except json.JSONDecodeError:
                                # JSON 파싱 실패 시 원본 텍스트 출력
                                print(content_item.text)
                        else:
                            # text 속성이 없는 경우 객체 자체 출력
                            print(content_item)
                elif hasattr(result, 'isError') and result.isError:
                    print("오류 응답:")
                    # isError가 True일 때 content가 있을 수 있음
                    if hasattr(result, 'content') and result.content:
                        for content_item in result.content:
                            if hasattr(content_item, 'text'):
                                print(content_item.text)
                            else:
                                print(content_item)
                    else: # 오류지만 content가 없는 경우
                        print("오류가 발생했으나 상세 내용이 없습니다.")
                elif hasattr(result, 'contents'):  # Resource 결과 형식
                    # Resource 형식의 결과 처리
                    for content in result.contents:
                        if hasattr(content, 'text'):
                            # JSON 형식 텍스트일 경우 파싱하여 예쁘게 출력 시도
                            try:
                                parsed_json = json.loads(content.text)
                                print(json.dumps(parsed_json, indent=2, ensure_ascii=False))
                            except json.JSONDecodeError:
                                # JSON 파싱 실패 시 원본 텍스트 출력
                                print(content.text)
                        else:
                            # text 속성이 없는 경우 객체 자체 출력
                            print(content)
                else:
                    # 예상치 못한 응답 형식
                    print("예상치 못한 응답 형식:")
                    print(result)

    except Exception as e:
        print(f"\n--- 클라이언트 오류 발생 ---")
        print(f"   오류 유형: {type(e).__name__}")
        print(f"   오류 메시지: {e}")

if __name__ == "__main__":
    # 터미널 인자 파싱
    if len(sys.argv) < 2:
        print(f"사용법: uv run client.py <name> [param1=value1] [param2=value2] ...")
        print("\n<name>은 다음 중 하나일 수 있습니다:")
        print("  1. Tool 이름")
        print("  2. Prompt 이름")
        print("  3. Resource 이름 또는 URI")
        print("\n사용 가능한 Tool 이름:")
        print("  search_videos, get_video_details, get_channel_details,")
        print("  get_video_comments, get_video_transcript, get_related_videos, get_trending_videos, get_video_enhanced_transcript")
        print("\n사용 가능한 Prompt 이름:")
        print("  transcript_summary")
        print("\n사용 가능한 Resource URI 예시:")
        print("  youtube://available-youtube-tools")
        print("  youtube://video/dQw4w9WgXcQ")
        print("  youtube://channel/UC_x5XG1OV2P6uZZ5FSM9Ttw")
        print("  youtube://transcript/dQw4w9WgXcQ?language=ko")
        print("\n파라미터 형식:")
        print("  key=value (띄어쓰기 없이)")
        print("\n예시:")
        print(f"  uv run client.py search_videos query=MCP max_results=5")
        print(f"  uv run client.py get_video_details video_id=zRgAEIoZEVQ")
        print(f"  uv run client.py get_channel_details channel_id=UCRpOIr-NJpK9S483ge20Pgw")
        print(f"  uv run client.py get_video_comments video_id=zRgAEIoZEVQ max_results=10 order=time")
        print(f"  uv run client.py get_video_transcript video_id=zRgAEIoZEVQ language=ko")
        print(f"  uv run client.py get_related_videos video_id=zRgAEIoZEVQ max_results=5")
        print(f"  uv run client.py get_trending_videos region_code=ko max_results=10")
        print(f"  uv run client.py get_video_enhanced_transcript video_ids=zRgAEIoZEVQ language=ko format=timestamped include_metadata=true start_time=100 end_time=200 query=에이전트 case_sensitive=true segment_method=equal segment_count=2")

        sys.exit(1)

    tool_name = sys.argv[1]
    arguments: Dict[str, Any] = {}

    # 추가 인자 파싱 (key=value)
    if len(sys.argv) > 2:
        for arg in sys.argv[2:]:
            if "=" in arg:
                key, value = arg.split("=", 1)
                key = key.strip()
                value = value.strip()

                # 배열 형태의 파라미터 처리 (쉼표로 구분)
                array_param_keys = ['video_ids']  # enhanced_transcript 도구는 video_ids를 리스트로 받음
                
                # 계층적 파라미터 처리 (예: filters.timeRange.start)
                if '.' in key:
                    parts = key.split('.')
                    # 첫 번째 계층이 없으면 생성
                    if parts[0] not in arguments:
                        arguments[parts[0]] = {}
                    
                    # 두 번째 계층이 없으면 생성
                    current = arguments[parts[0]]
                    for i in range(1, len(parts) - 1):
                        if parts[i] not in current:
                            current[parts[i]] = {}
                        current = current[parts[i]]
                    
                    # 값 설정 (타입 변환 적용)
                    final_key = parts[-1]
                    if value.isdigit():
                        current[final_key] = int(value)
                    elif value.lower() in ['true', 'false']:
                        current[final_key] = value.lower() == 'true'
                    else:
                        current[final_key] = value
                # 배열 파라미터 처리
                elif key in array_param_keys:
                    arguments[key] = value.split(',')
                # 숫자형 파라미터 처리
                elif key in ['max_results'] and value.isdigit():
                    arguments[key] = int(value)
                # 불리언 파라미터 처리
                elif key in ['include_replies', 'include_metadata'] and value.lower() in ['true', 'false']:
                    arguments[key] = value.lower() == 'true'
                # 그 외 일반 문자열 파라미터
                else:
                    arguments[key] = value
            else:
                print(f"경고: 잘못된 파라미터 형식 무시됨 - '{arg}'. 'key=value' 형식을 사용하세요.")

    # 비동기 함수 실행
    try:
        asyncio.run(run_tool_call(tool_name, arguments))
    except KeyboardInterrupt:
        logger.info("사용자에 의해 클라이언트 실행이 중단되었습니다.")
