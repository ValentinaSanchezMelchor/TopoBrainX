FROM python:3.12-slim

# Install OpenJDK 21 runtime
RUN apt-get update \
 && apt-get install -y --no-install-recommends openjdk-21-jre-headless ca-certificates \
 && rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64
ENV PATH="$JAVA_HOME/bin:${PATH}"

WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt || true
COPY . .
CMD ["python", "scripts/run_oinfo_sinfo_triplets_1subject.py"]