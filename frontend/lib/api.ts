const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL;

export async function loginUser(email: string, password: string) {
    const response = await fetch(`${API_BASE_URL}/auth/login`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({email, password}),
    });

    if (!response.ok) {
        throw new Error("Invalid email or password");
    }

    return response.json();
}

export async function registerUser(name: string, email: string, password: string) {
    const response = await fetch(`${API_BASE_URL}/auth/register`, {
        method: "POST",
        headers: {
        "Content-Type": "application/json"
        },
        body: JSON.stringify({ name, email, password }),
    });

    if (!response.ok) {
        throw new Error("Registration failed");
    }

    return response.json();
}
