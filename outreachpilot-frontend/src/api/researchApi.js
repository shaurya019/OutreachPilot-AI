import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 120000,
  headers: {
    "Content-Type": "application/json",
  },
});

export async function startResearch(payload) {
  const response = await api.post("/research/start", payload);
  return response.data;
}

export async function getResearchReport(reportId) {
  const response = await api.get(`/research/${reportId}`);
  return response.data;
}

export async function approveOutreach(reportId) {
  const response = await api.post(`/research/${reportId}/approve`);
  return response.data;
}

export async function rejectOutreach(reportId) {
  const response = await api.post(`/research/${reportId}/reject`);
  return response.data;
}

export async function regenerateReport(reportId) {
  const response = await api.post(`/research/${reportId}/regenerate`);
  return response.data;
}