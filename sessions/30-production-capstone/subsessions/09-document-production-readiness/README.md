# Sub-Session 09: Document Production Readiness

This sub-session closes the course by turning the capstone work into an
operator-ready handoff.

## Goal

Create a production readiness summary for the message board app.

## App-Based Lab

Use the live capstone deployment as evidence. The final document should include
the app topology, ownership boundaries, release process, rollback process,
security controls, scaling assumptions, observability, backup plan, and open
risks.

## Check

```bash
kubectl get all -n message-board-prod
kubectl get ingress,gateway,httproute -n message-board-prod
kubectl get networkpolicy,pdb,hpa,servicemonitor,prometheusrule -n message-board-prod
kubectl get events -n message-board-prod --sort-by=.lastTimestamp
```

## Cleanup

```bash
kubectl delete namespace message-board-prod --ignore-not-found
```

## Review Prompts

1. What is the exact rollback command for the frontend?
2. Which alerts prove user impact?
3. Which known risks remain before a real production launch?
