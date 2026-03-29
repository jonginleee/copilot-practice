"""데이터 처리 모듈"""

def process_items(items):
    """항목을 처리합니다."""
    result = []
    for item in items:
        if item['status'] == 'active':
            # 복잡한 처리 로직
            processed = {
                'id': item['id'],
                'name': item['name'].upper(),
                'value': item['value'] * 1.1,
                'timestamp': item.get('timestamp')
            }
            result.append(processed)
    return result

def calculate_statistics(data):
    """통계를 계산합니다."""
    if not data:
        return None
    
    total = sum(d['value'] for d in data)
    count = len(data)
    average = total / count
    
    return {
        'total': total,
        'average': average,
        'count': count
    }
