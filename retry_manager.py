from typing import List
from .models import TrackingResult, ContainerQuery

def get_failed(results: List[TrackingResult]) -> List[ContainerQuery]:
    failed = []
    for r in results:
        if not r.success:
            failed.append(ContainerQuery(container_no=r.container_no, carrier=r.carrier))
    return failed
