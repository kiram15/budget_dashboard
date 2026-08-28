import { Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import HouseDashboard from './pages/HouseDashboard'
import Investments from './pages/Investments'
import Savings from './pages/Savings'
import Spending from './pages/Spending'
import Breakdown from './pages/Breakdown'

export default function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route path="/" element={<Breakdown />} />
        <Route path="/investments" element={<Investments />} />
        <Route path="/savings" element={<Savings />} />
        <Route path="/spending" element={<Spending />} />
        <Route path="/house" element={<HouseDashboard />} />
      </Route>
    </Routes>
  )
}
