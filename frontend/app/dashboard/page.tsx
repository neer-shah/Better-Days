"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { getDashboard } from "@/lib/api";
import { getToken, logout } from "@/lib/auth";
import type { DashboardResponse } from "@/types/dashboard";

export default function DashboardPage() {
  const router = useRouter();

  const [dashboard, setDashboard] = useState<DashboardResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadDashboard() {
      const token = getToken();

      if (!token) {
        router.push("/login");
        return;
      }

      try {
        const data = await getDashboard(token);
        setDashboard(data);
      } catch {
        setError("Could not load dashboard.");
      } finally {
        setLoading(false);
      }
    }

    loadDashboard();
  }, [router]);

  function handleLogout() {
    logout();
    router.push("/login");
  }

  if (loading) {
    return (
      <main className="min-h-screen bg-slate-50 p-8">
        <p>Loading dashboard...</p>
      </main>
    );
  }

  if (error || !dashboard) {
    return (
      <main className="min-h-screen bg-slate-50 p-8">
        <p className="text-red-600">{error || "Dashboard unavailable."}</p>
      </main>
    );
  }

  const { summary, recent_checkins } = dashboard;

  return (
    <main className="min-h-screen bg-slate-50 p-6">
      <div className="mx-auto max-w-5xl">
        <div className="mb-8 flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-semibold text-slate-900">
              Better Days Dashboard
            </h1>
            <p className="mt-1 text-slate-600">
              A quick snapshot of your recent wellbeing check-ins.
            </p>
          </div>

          <button
            onClick={handleLogout}
            className="rounded-lg border border-slate-300 px-4 py-2 text-sm text-slate-700 hover:bg-white"
          >
            Log out
          </button>
        </div>

        <section className="grid gap-4 md:grid-cols-4">
          <SummaryCard
            label="Total check-ins"
            value={summary.total_checkins.toString()}
          />
          <SummaryCard
            label="Average mood"
            value={summary.average_mood?.toString() ?? "—"}
          />
          <SummaryCard
            label="Average stress"
            value={summary.average_stress?.toString() ?? "—"}
          />
          <SummaryCard
            label="Average sleep"
            value={
              summary.average_sleep_hours !== null
                ? `${summary.average_sleep_hours}h`
                : "—"
            }
          />
        </section>

        <section className="mt-8 rounded-2xl bg-white p-6 shadow-sm">
          <div className="mb-4 flex items-center justify-between">
            <h2 className="text-xl font-semibold text-slate-900">
              Recent check-ins
            </h2>
            <button
              onClick={() => router.push("/checkin")}
              className="rounded-lg bg-slate-900 px-4 py-2 text-sm text-white"
            >
              Add check-in
            </button>
          </div>

          {recent_checkins.length === 0 ? (
            <p className="text-slate-600">
              No check-ins yet. Add your first one to start seeing trends.
            </p>
          ) : (
            <div className="space-y-3">
              {recent_checkins.map((checkin) => (
                <div
                  key={checkin.id}
                  className="rounded-xl border border-slate-200 p-4"
                >
                  <div className="flex items-center justify-between">
                    <p className="font-medium text-slate-900">
                      {checkin.date}
                    </p>
                    <p className="text-sm text-slate-600">
                      Mood {checkin.mood} · Stress {checkin.stress} · Energy{" "}
                      {checkin.energy}
                    </p>
                  </div>
                  <p className="mt-2 text-slate-700">
                    Small win: {checkin.small_win}
                  </p>
                </div>
              ))}
            </div>
          )}
        </section>
      </div>
    </main>
  );
}

function SummaryCard({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-2xl bg-white p-5 shadow-sm">
      <p className="text-sm text-slate-500">{label}</p>
      <p className="mt-2 text-2xl font-semibold text-slate-900">{value}</p>
    </div>
  );
}
