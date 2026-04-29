from datetime import datetime

from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    "Operations Status MCP",
    stateless_http=True,
    json_response=True,
)


@mcp.tool()
def get_ops_status() -> dict:
    """
    오늘의 운영 데이터 현황을 반환합니다.

    포함 항목:
    - 주문 수와 실패율
    - 결제 성공/실패 현황
    - 고객지원 티켓 현황
    - API 오류율, 지연 시간, 진행 중인 인시던트
    """
    return {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "orders": {
            "total": 1284,
            "failed": 17,
            "failure_rate": 1.32,
        },
        "payments": {
            "success": 1198,
            "failed": 22,
            "failure_rate": 1.8,
        },
        "support": {
            "new_tickets": 43,
            "urgent_tickets": 5,
            "avg_first_response_minutes": 18,
        },
        "system": {
            "api_error_rate": 0.7,
            "p95_latency_ms": 420,
            "active_incidents": 1,
        },
    }


@mcp.tool()
def get_ops_alerts() -> list[dict]:
    """
    운영 지표에서 주의가 필요한 항목을 반환합니다.

    기준:
    - 결제 실패율 1.5% 이상
    - 긴급 티켓 5건 이상
    - 진행 중인 인시던트 1건 이상
    """
    status = get_ops_status()
    alerts: list[dict] = []

    if status["payments"]["failure_rate"] >= 1.5:
        alerts.append(
            {
                "level": "warning",
                "area": "payments",
                "message": "결제 실패율이 기준치보다 높습니다.",
                "value": status["payments"]["failure_rate"],
                "threshold": 1.5,
            }
        )

    if status["support"]["urgent_tickets"] >= 5:
        alerts.append(
            {
                "level": "warning",
                "area": "support",
                "message": "긴급 티켓 수가 많습니다.",
                "value": status["support"]["urgent_tickets"],
                "threshold": 5,
            }
        )

    if status["system"]["active_incidents"] > 0:
        alerts.append(
            {
                "level": "critical",
                "area": "system",
                "message": "진행 중인 인시던트가 있습니다.",
                "value": status["system"]["active_incidents"],
                "threshold": 0,
            }
        )

    return alerts


@mcp.tool()
def get_ops_briefing() -> str:
    """운영 리더에게 공유할 수 있는 짧은 현황 브리핑을 반환합니다."""
    status = get_ops_status()
    alerts = get_ops_alerts()

    critical_count = sum(1 for alert in alerts if alert["level"] == "critical")

    return (
        f"{status['date']} 운영 현황: "
        f"주문 {status['orders']['total']}건, "
        f"결제 실패율 {status['payments']['failure_rate']}%, "
        f"긴급 티켓 {status['support']['urgent_tickets']}건, "
        f"진행 중인 인시던트 {status['system']['active_incidents']}건입니다. "
        f"알림은 총 {len(alerts)}건이며 critical은 {critical_count}건입니다."
    )


if __name__ == "__main__":
    mcp.run(transport="streamable-http")