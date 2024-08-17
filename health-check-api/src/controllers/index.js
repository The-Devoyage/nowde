import express from "express";
import HealthController from "./HealthController.js";

const router = express.Router();
router.use("/HealthController", HealthController);

export default router;
