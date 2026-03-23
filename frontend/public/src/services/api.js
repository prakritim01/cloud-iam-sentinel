import axios from "axios";

export const scanPolicy = async (policy) => {
  const res = await axios.post("http://localhost:8000/scan", { policy });
  return res.data;
};