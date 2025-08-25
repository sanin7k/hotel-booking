export default function GoogleLogin() {
    const handleGoogleLogin = async () => {
    window.location.href = `${import.meta.env.VITE_API_URL}/login/google`;
  };

  return (
    <button
          onClick={handleGoogleLogin}
          className="flex items-center justify-center gap-2 px-4 py-2 border rounded"
        >
          <img
            src="https://developers.google.com/identity/images/g-logo.png"
            alt="Google logo"
            className="w-5 h-5"
          />
          <span>Sign in with Google</span>
        </button>
  )
}