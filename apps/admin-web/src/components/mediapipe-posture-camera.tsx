'use client';

import { DrawingUtils, FilesetResolver, PoseLandmarker } from '@mediapipe/tasks-vision';
import { useEffect, useRef, useState } from 'react';
import { endpoints } from '@/lib/api';
import { useAuth } from '@/stores/auth';
import { Button, Card, Input } from './ui';

type LandmarkPayload = { name: string; x: number; y: number; z?: number; visibility?: number };
const landmarkNames = ['nose','left_eye_inner','left_eye','left_eye_outer','right_eye_inner','right_eye','right_eye_outer','left_ear','right_ear','mouth_left','mouth_right','left_shoulder','right_shoulder','left_elbow','right_elbow','left_wrist','right_wrist','left_pinky','right_pinky','left_index','right_index','left_thumb','right_thumb','left_hip','right_hip','left_knee','right_knee','left_ankle','right_ankle','left_heel','right_heel','left_foot_index','right_foot_index'];

export function MediaPipePostureCamera() {
  const token = useAuth((state) => state.accessToken);
  const videoRef = useRef<HTMLVideoElement | null>(null);
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const landmarkerRef = useRef<PoseLandmarker | null>(null);
  const rafRef = useRef<number | null>(null);
  const [organizationId, setOrganizationId] = useState('');
  const [memberId, setMemberId] = useState('');
  const [status, setStatus] = useState('Idle');
  const [lastResult, setLastResult] = useState('');

  useEffect(() => () => { if (rafRef.current) cancelAnimationFrame(rafRef.current); void stopCamera(); }, []);

  async function initializeModel() {
    if (landmarkerRef.current) return landmarkerRef.current;
    setStatus('Loading MediaPipe PoseLandmarker...');
    const resolver = await FilesetResolver.forVisionTasks('https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@latest/wasm');
    landmarkerRef.current = await PoseLandmarker.createFromOptions(resolver, {
      baseOptions: {
        modelAssetPath: 'https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_lite/float16/latest/pose_landmarker_lite.task',
        delegate: 'GPU',
      },
      runningMode: 'VIDEO',
      numPoses: 1,
    });
    return landmarkerRef.current;
  }

  async function startCamera() {
    if (!organizationId || !memberId) { setStatus('Organization ID and Member ID are required.'); return; }
    const landmarker = await initializeModel();
    const stream = await navigator.mediaDevices.getUserMedia({ video: { width: 960, height: 540 }, audio: false });
    const video = videoRef.current;
    if (!video) return;
    video.srcObject = stream;
    await video.play();
    setStatus('Analyzing live camera feed...');
    const loop = async () => {
      if (!videoRef.current || !canvasRef.current) return;
      const result = landmarker.detectForVideo(videoRef.current, performance.now());
      draw(result.landmarks?.[0] ?? []);
      if (result.landmarks?.[0]?.length) await sendFrame(result.landmarks[0]);
      rafRef.current = requestAnimationFrame(loop);
    };
    rafRef.current = requestAnimationFrame(loop);
  }

  async function stopCamera() {
    if (rafRef.current) cancelAnimationFrame(rafRef.current);
    rafRef.current = null;
    const stream = videoRef.current?.srcObject as MediaStream | null;
    stream?.getTracks().forEach((track) => track.stop());
    if (videoRef.current) videoRef.current.srcObject = null;
    setStatus('Camera stopped');
  }

  async function sendFrame(raw: Array<{ x: number; y: number; z?: number; visibility?: number }>) {
    const landmarks: LandmarkPayload[] = raw.map((item, index) => ({ name: landmarkNames[index] ?? `landmark_${index}`, x: item.x, y: item.y, z: item.z, visibility: item.visibility }));
    try {
      const response = await endpoints.create('posture/analyze-frame', { organizationId, memberId, exerciseType: 'squat', landmarks }, token);
      setLastResult(JSON.stringify(response, null, 2));
    } catch (error) {
      setLastResult(error instanceof Error ? error.message : String(error));
    }
  }

  function draw(landmarks: Array<{ x: number; y: number; z?: number; visibility?: number }>) {
    const canvas = canvasRef.current;
    const video = videoRef.current;
    if (!canvas || !video) return;
    canvas.width = video.videoWidth || 960;
    canvas.height = video.videoHeight || 540;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    const drawingUtils = new DrawingUtils(ctx);
    const normalized = landmarks.map((landmark) => ({ ...landmark, z: landmark.z ?? 0, visibility: landmark.visibility ?? 1 }));
    drawingUtils.drawLandmarks(normalized, { radius: 4, color: '#d4af37' });
    drawingUtils.drawConnectors(normalized, PoseLandmarker.POSE_CONNECTIONS, { color: '#22c55e', lineWidth: 2 });
  }

  return <Card className="space-y-4"><h3 className="text-xl font-bold">MediaPipe Live Posture Camera</h3><div className="grid gap-3 md:grid-cols-2"><Input placeholder="Organization ID" value={organizationId} onChange={(e)=>setOrganizationId(e.target.value)} /><Input placeholder="Member ID" value={memberId} onChange={(e)=>setMemberId(e.target.value)} /></div><div className="flex gap-2"><Button onClick={startCamera}>Start MediaPipe Camera</Button><Button onClick={stopCamera}>Stop</Button></div><p className="text-sm text-zinc-400">{status}</p><div className="relative overflow-hidden rounded-2xl border border-white/10"><video ref={videoRef} className="w-full" playsInline muted /><canvas ref={canvasRef} className="absolute inset-0 h-full w-full" /></div><pre className="max-h-80 overflow-auto rounded-xl bg-black/40 p-3 text-xs">{lastResult}</pre></Card>;
}
