import express from "express";
const router = express.Router();
import { HealthCheckService } from "../services/HealthCheckService/index.js";

router.get("/", async (req, res) => {
  try {
    let finalData = {};
    const HealthCheckServiceData = await HealthCheckService();
    finalData["HealthCheckService"] = HealthCheckServiceData;

    res.json(finalData);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

export default router;
