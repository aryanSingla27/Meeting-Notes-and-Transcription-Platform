import "./globals.css";
import type { Metadata } from "next";
import { Sidebar } from "../components/Sidebar";
import { Topbar } from "../components/Topbar";
import { ThemeProvider } from "../components/ThemeProvider";

export const metadata: Metadata = {
  title: "Meetings | Fireflies Workspace",
  description: "Meeting notes, transcripts, summaries and action items.",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="en" suppressHydrationWarning><body><ThemeProvider><div className="app"><Sidebar /><main className="main"><Topbar />{children}</main></div></ThemeProvider></body></html>;
}
