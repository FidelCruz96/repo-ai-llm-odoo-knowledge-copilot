import http from "k6/http";
import { check, sleep } from "k6";

const url = __ENV.QUERY_URL || "http://localhost:8000/v1/query";
const apiKey = __ENV.API_KEY || "change-me";
const queryText = __ENV.LOAD_TEST_QUERY || "¿Qué es un picking en Odoo?";

export const options = {
  vus: Number(__ENV.VUS || 10),
  duration: __ENV.DURATION || "30s",
  thresholds: {
    http_req_failed: ["rate<0.01"],
    http_req_duration: ["p(95)<3000"],
  },
};

export default function () {
  const payload = JSON.stringify({
    query: queryText,
    stream: false,
  });

  const params = {
    headers: {
      "Content-Type": "application/json",
      "X-API-Key": apiKey,
    },
  };

  const response = http.post(url, payload, params);
  check(response, {
    "status is 200": (r) => r.status === 200,
    "has answer field": (r) => {
      try {
        return Boolean(r.json("answer"));
      } catch (_) {
        return false;
      }
    },
  });

  sleep(0.5);
}
