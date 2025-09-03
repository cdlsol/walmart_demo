FROM python:3.11-slim
WORKDIR /app

RUN pip install --no-cache-dir uv

# Install MetricFlow MCP + Postgres adapter into system Python
RUN uv pip install --system "dbt-metricflow[mcp]==0.8.2" dbt-postgres

# Copy dbt project + profiles
COPY ./demo_walmart/vs_demo_walmart /app/vs_demo_walmart
COPY ./demo_walmart/mcp/.dbt /root/.dbt

# RUN uv add dbt-metricflow[mcp]

EXPOSE 8080

CMD ["uv", "run", "mf", "mcp", "serve", "--dbt-project-dir", "/app/vs_demo_walmart", "--profiles-dir", "/root/.dbt", "--port", "8080"]
