import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import AvailabilityCalendar from "./pages/AvailabilityCalendar";
import Navbar from "./components/Navbar";

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <Navbar />
        <div className="container mx-auto px-4 py-8">
          <Routes>
            <Route path="/" element={<AvailabilityCalendar />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
