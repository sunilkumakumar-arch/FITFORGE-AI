import 'dart:async';
import 'package:camera/camera.dart';
import 'package:flutter/material.dart';
import 'package:google_mlkit_pose_detection/google_mlkit_pose_detection.dart';
import '../app.dart';

class PostureCaptureScreen extends StatefulWidget { const PostureCaptureScreen({super.key}); @override State<PostureCaptureScreen> createState()=>_PostureCaptureScreenState(); }
class _PostureCaptureScreenState extends State<PostureCaptureScreen>{
  final organizationId=TextEditingController();
  final memberId=TextEditingController();
  final poseDetector = PoseDetector(options: PoseDetectorOptions(mode: PoseDetectionMode.stream));
  CameraController? controller;
  bool processing=false;
  String result='';

  @override void dispose(){ controller?.dispose(); poseDetector.close(); super.dispose(); }

  Future<void> startCamera() async {
    final cameras = await availableCameras();
    if (cameras.isEmpty) { setState(()=>result='No camera available'); return; }
    controller = CameraController(cameras.first, ResolutionPreset.medium, enableAudio: false);
    await controller!.initialize();
    await controller!.startImageStream(processFrame);
    setState((){});
  }

  Future<void> processFrame(CameraImage image) async {
    if (processing || organizationId.text.isEmpty || memberId.text.isEmpty) return;
    processing = true;
    try {
      final inputImage = _inputImageFromCameraImage(image);
      if (inputImage == null) return;
      final poses = await poseDetector.processImage(inputImage);
      if (poses.isEmpty) return;
      final response = await AppScope.of(context).api.post('/posture/analyze-frame', {
        'organizationId': organizationId.text,
        'memberId': memberId.text,
        'exerciseType': 'squat',
        'landmarks': poses.first.landmarks.entries.map((entry)=>{'name': entry.key.name, 'x': entry.value.x, 'y': entry.value.y, 'z': entry.value.z, 'visibility': entry.value.likelihood}).toList(),
      });
      if (mounted) setState(()=>result=response.toString());
    } finally { processing = false; }
  }

  InputImage? _inputImageFromCameraImage(CameraImage image) {
    if (controller == null) return null;
    final camera = controller!.description;
    final rotation = InputImageRotationValue.fromRawValue(camera.sensorOrientation);
    final format = InputImageFormatValue.fromRawValue(image.format.raw);
    if (rotation == null || format == null || image.planes.isEmpty) return null;
    return InputImage.fromBytes(
      bytes: image.planes.first.bytes,
      metadata: InputImageMetadata(size: Size(image.width.toDouble(), image.height.toDouble()), rotation: rotation, format: format, bytesPerRow: image.planes.first.bytesPerRow),
    );
  }

  Future<void> analyzeDemo() async {
    final response=await AppScope.of(context).api.post('/posture/analyze-frame', {'organizationId':organizationId.text,'memberId':memberId.text,'exerciseType':'squat','landmarks':[{'name':'left_hip','x':0,'y':0,'visibility':1},{'name':'left_knee','x':0,'y':1,'visibility':1},{'name':'left_ankle','x':1,'y':1,'visibility':1}]});
    setState(()=>result=response.toString());
  }

  @override Widget build(BuildContext context){ return Scaffold(appBar: AppBar(title: const Text('AI Posture Capture')), body: ListView(padding: const EdgeInsets.all(16), children:[TextField(controller: organizationId, decoration: const InputDecoration(labelText:'Organization ID')), TextField(controller: memberId, decoration: const InputDecoration(labelText:'Member ID')), const SizedBox(height:16), if(controller?.value.isInitialized == true) AspectRatio(aspectRatio: controller!.value.aspectRatio, child: CameraPreview(controller!)), const SizedBox(height:16), FilledButton(onPressed:startCamera, child: const Text('Start Camera Pose Detection')), const SizedBox(height:8), OutlinedButton(onPressed:analyzeDemo, child: const Text('Analyze Demo Frame')), Text(result)])); }
}
