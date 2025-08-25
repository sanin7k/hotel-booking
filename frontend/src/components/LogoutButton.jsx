import { useNavigate } from "react-router-dom";
import api from "../api/axios"

export default function LogoutButton() {
    const navigate = useNavigate()

    const handleLogout = async () => {
        try {
            await api.get("/logout")
            navigate("/login")
        } catch (error) {
            console.error("Logout failed", error)
        }
    }

    return (
        <button
            className="text-blue-600 hover:underline"
            onClick={handleLogout}
          >
            Logout
          </button>
    )
}