import { useState, useRef } from 'react';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Tabs, TabsList, TabsTrigger, TabsContent } from '@/components/ui/tabs';
import { Mic, MicOff, FileAudio, Loader2 } from 'lucide-react';
import type { InputType } from '@/types';

interface ProblemReportFormProps {
  onSubmit: (inputType: InputType, problemText?: string, audioFile?: File) => void;
  isSubmitting: boolean;
}

export function ProblemReportForm({ onSubmit, isSubmitting }: ProblemReportFormProps) {
  const [inputType, setInputType] = useState<InputType>('TEXT');
  const [problemText, setProblemText] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const [audioBlob, setAudioBlob] = useState<Blob | null>(null);
  const [recordingTime, setRecordingTime] = useState(0);
  
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const timerRef = useRef<number | null>(null);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;

      const chunks: Blob[] = [];
      mediaRecorder.ondataavailable = (e) => {
        if (e.data.size > 0) {
          chunks.push(e.data);
        }
      };

      mediaRecorder.onstop = () => {
        const blob = new Blob(chunks, { type: 'audio/webm' });
        setAudioBlob(blob);
        stream.getTracks().forEach(track => track.stop());
      };

      mediaRecorder.start();
      setIsRecording(true);
      setRecordingTime(0);

      // Start timer
      timerRef.current = window.setInterval(() => {
        setRecordingTime(prev => prev + 1);
      }, 1000);
    } catch (error) {
      console.error('Error accessing microphone:', error);
      alert('Could not access microphone. Please check permissions.');
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
      if (timerRef.current) {
        window.clearInterval(timerRef.current);
      }
    }
  };

  const handleSubmit = () => {
    if (inputType === 'TEXT' && problemText.trim()) {
      onSubmit('TEXT', problemText);
      setProblemText('');
    } else if (inputType === 'VOICE' && audioBlob) {
      const audioFile = new File([audioBlob], 'recording.webm', { type: 'audio/webm' });
      onSubmit('VOICE', undefined, audioFile);
      setAudioBlob(null);
      setRecordingTime(0);
    }
  };

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const canSubmit = (inputType === 'TEXT' && problemText.trim()) || (inputType === 'VOICE' && audioBlob);

  return (
    <Card className="p-6">
      <h2 className="text-2xl font-bold mb-4">Report a Problem</h2>
      <p className="text-muted-foreground mb-6">
        Describe your problem and get AI-powered recommendations
      </p>

      <Tabs value={inputType} onValueChange={(value) => setInputType(value as InputType)}>
        <TabsList className="grid w-full grid-cols-2">
          <TabsTrigger value="TEXT">Text Input</TabsTrigger>
          <TabsTrigger value="VOICE">Voice Recording</TabsTrigger>
        </TabsList>

        <TabsContent value="TEXT" className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="problem">Describe your problem</Label>
            <Textarea
              id="problem"
              placeholder="Enter your problem description..."
              value={problemText}
              onChange={(e) => setProblemText(e.target.value)}
              rows={6}
              disabled={isSubmitting}
            />
          </div>
        </TabsContent>

        <TabsContent value="VOICE" className="space-y-4">
          <div className="space-y-4">
            <div className="flex flex-col items-center justify-center p-8 border-2 border-dashed rounded-lg">
              {!isRecording && !audioBlob && (
                <Button onClick={startRecording} size="lg" disabled={isSubmitting}>
                  <Mic className="h-5 w-5 mr-2" />
                  Start Recording
                </Button>
              )}

              {isRecording && (
                <div className="text-center space-y-4">
                  <div className="flex items-center justify-center">
                    <div className="animate-pulse">
                      <Mic className="h-12 w-12 text-red-500" />
                    </div>
                  </div>
                  <p className="text-lg font-semibold">{formatTime(recordingTime)}</p>
                  <Button onClick={stopRecording} variant="destructive">
                    <MicOff className="h-5 w-5 mr-2" />
                    Stop Recording
                  </Button>
                </div>
              )}

              {audioBlob && !isRecording && (
                <div className="text-center space-y-4">
                  <FileAudio className="h-12 w-12 mx-auto text-primary" />
                  <p className="text-sm text-muted-foreground">
                    Recording ready ({formatTime(recordingTime)})
                  </p>
                  <Button onClick={startRecording} variant="outline">
                    <Mic className="h-5 w-5 mr-2" />
                    Record Again
                  </Button>
                </div>
              )}
            </div>
          </div>
        </TabsContent>
      </Tabs>

      <div className="mt-6">
        <Button 
          onClick={handleSubmit} 
          disabled={!canSubmit || isSubmitting}
          className="w-full"
        >
          {isSubmitting ? (
            <>
              <Loader2 className="h-4 w-4 mr-2 animate-spin" />
              Processing...
            </>
          ) : (
            'Get Recommendations'
          )}
        </Button>
      </div>
    </Card>
  );
}
