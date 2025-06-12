# Interview Appointment Scheduling Frontend

This is a frontend single page app for the Appointment Scheduling application. It provides a user interface
to show an advisors availability.

## Features

- Responsive UI built with React and Tailwind CSS
- Type-safe development with TypeScript

## Getting Started

### Prerequisites

- Node.js (v14+)
- npm (v6+)

### Run the Development Server in Your Local Machine

1. Clone the repository
2. Navigate to the frontend directory:
   ```
   cd interview-calendar-frontend
   ```
3. Install dependencies:
   ```
   npm install
   ```
4. Start the development server:
   ```
   npm run dev
   ```

## API Integration

The frontend is designed to work with the Django backend that's in the peer folder. It includes:

- Mock data for displaying interviews
- Placeholders for API calls that can be easily connected to the backend
- Form for scheduling new interviews
- TypeScript interfaces for type safety

To access the backend endpoints, make sure that you have started the local backend server. These are the paths

- `/api/users/`
- `/api/users/1/calendar/free/`

## Notes for Interview Candidates

This frontend is part of an interview assignment. Your task may include:

1. Connecting the frontend to the Django backend
2. Implementing additional features
3. Improving the UI/UX
4. Adding validation or error handling
5. Testing

Feel free to modify the code as needed for your assignment.
