export interface Appointment {
  id: number;
  title: string;
  date: string;
  duration: number;
  status: 'scheduled' | 'cancelled' | 'completed';
  interviewee: string;
  interviewer: string;
  notes?: string;
}

export interface AppointmentFormData {
  title: string;
  date: string;
  time: string;
  duration: number;
  interviewee: string;
  interviewer: string;
  notes: string;
} 