export type InputType = 'TEXT' | 'VOICE';

export interface ProblemReport {
  id: number;
  user: number;
  input_type: InputType;
  problem_text: string;
  audio_file: string | null;
  recommendations: string[];
  created_at: string;
}

export interface CreateProblemReportData {
  input_type: InputType;
  problem_text?: string;
  audio_file?: File;
}
