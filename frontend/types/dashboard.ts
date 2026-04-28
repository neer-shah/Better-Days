export type DashboardSummary = {
    total_checkins: number;
    average_mood: number | null;
    average_stress: number | null;
    average_sleep_hours: number | null;
    latest_checkin_date: string | null;
};

export type DashboardTrendPoint = {
    date: string;
    mood: number;
    stress: number;
    energy: number;
    sleep_hours: number;
    productivity: number;
};

export type RecentCheckinItem = {
    id: number;
    date: string;
    mood: number;
    stress: number;
    energy: number;
    small_win: string;
};

export type DashboardResponse = {
    summary: DashboardSummary;
    trends: DashboardTrendPoint[];
    recent_checkins: RecentCheckinItem[];
};
