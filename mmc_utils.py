# Auto-generated M/M/C Queuing Model utilities - 2026-08-13
# Queuing System Implementation - Optimization using M/M/C Model

import math
import datetime
from typing import Optional

MODULE_VERSION = "1.0.4"
GENERATED_DATE = "2026-08-13"


def erlang_c(c: int, rho: float) -> float:
    """
    Compute the Erlang C formula probability (P_wait).
    c: number of servers
    rho: traffic intensity = lambda / (c * mu)
    Returns probability that a customer has to wait.
    """
    a = c * rho  # offered load
    sum_terms = sum((a ** k) / math.factorial(k) for k in range(c))
    erlang_b_inv = sum_terms + (a ** c) / (math.factorial(c) * (1 - rho))
    p0 = 1 / erlang_b_inv
    p_wait = ((a ** c) / (math.factorial(c) * (1 - rho))) * p0
    return round(p_wait, 6)


def average_wait_time(lam: float, mu: float, c: int) -> Optional[float]:
    """
    Compute average waiting time in queue (Wq) for M/M/C model.
    lam: arrival rate (customers per unit time)
    mu: service rate per server
    c: number of servers
    """
    rho = lam / (c * mu)
    if rho >= 1:
        return None  # System unstable
    p_wait = erlang_c(c, rho)
    wq = p_wait / (c * mu - lam)
    return round(wq, 6)


def system_utilization(lam: float, mu: float, c: int) -> float:
    """Return server utilization (rho)."""
    return round(lam / (c * mu), 4)


def average_queue_length(lam: float, mu: float, c: int) -> Optional[float]:
    """Compute average number of customers in queue (Lq)."""
    wq = average_wait_time(lam, mu, c)
    if wq is None:
        return None
    return round(lam * wq, 4)


def run_simulation_summary(lam: float, mu: float, c: int) -> dict:
    """Run a complete M/M/C model summary."""
    rho = system_utilization(lam, mu, c)
    wq = average_wait_time(lam, mu, c)
    lq = average_queue_length(lam, mu, c)
    return {
        "arrival_rate": lam,
        "service_rate": mu,
        "servers": c,
        "utilization": rho,
        "avg_wait_time_in_queue": wq,
        "avg_customers_in_queue": lq,
        "stable": rho < 1,
        "computed_at": datetime.datetime.utcnow().isoformat()
    }


if __name__ == "__main__":
    result = run_simulation_summary(lam=10, mu=4, c=3)
    for k, v in result.items():
        print(f"{k}: {v}")
