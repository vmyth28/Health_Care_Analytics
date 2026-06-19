import axios from "axios";

const API = axios.create({
  baseURL: "http://localhost:8000",
});

export const testBackend = async () => (await API.get("/api/test")).data;
export const uploadCsv = async (formData) => (await API.post("/upload", formData)).data;
export const addRecord = async (payload) => (await API.post("/records", payload)).data;
export const getRecentRecords = async () => (await API.get("/records/recent")).data;
export const getSummary = async () => (await API.get("/analytics/summary")).data;
export const getPatientTrends = async () => (await API.get("/analytics/patient-trends")).data;
export const getDiseaseDistribution = async () => (await API.get("/analytics/disease-distribution")).data;
export const getHospitalPerformance = async () => (await API.get("/analytics/hospital-performance")).data;
export const getClaimCosts = async () => (await API.get("/analytics/claim-costs")).data;
export const getClaimStatus = async () => (await API.get("/analytics/claim-status")).data;
export const getInsights = async () => (await API.get("/analytics/insights")).data;
export const trainModel = async () => (await API.post("/ml/train")).data;
export const predictClaim = async (payload) => (await API.post("/ml/predict-claim", payload)).data;

export default API;
