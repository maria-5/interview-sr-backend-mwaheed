import { useState } from "react";

const AvailabilityCalendar = () => {
  const [timeSlots] = useState([
    {
      start: "2025-05-05T16:00:00+00:00",
      end: "2025-05-05T18:00:00+00:00",
      day_of_week: "Monday",
    },
  ]);

  const DAY_OF_THE_WEEK = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"];

  // Group by day
  const calendarDays = DAY_OF_THE_WEEK.map((day) => ({
    name: day,
    slots: timeSlots.filter((slot) => slot.day_of_week === day),
  }));

  return (
    <div>
      <h1 className="text-xl font-bold text-gray-800 mb-6">Available Time Slots</h1>

      <div className="bg-white p-6 rounded-lg shadow-md">
        <ul className="grid grid-cols-7 gap-4">
          {calendarDays.map((day) => (
            <li key={day.name} className="border rounded-lg p-3">
              <div className="font-semibold text-center bg-gray-100 p-2 mb-3 rounded">{day.name}</div>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default AvailabilityCalendar;
