"use client";
import { createContext, useContext, useEffect, useState } from "react";
type Theme = "light" | "dark";
const ThemeContext = createContext<{theme:Theme; toggle:()=>void}>({theme:"light",toggle:()=>{}});
export function ThemeProvider({children}:{children:React.ReactNode}) {
  const [theme,setTheme] = useState<Theme>("light");
  useEffect(()=>{ const saved=localStorage.getItem("noteflow-theme"); const initial=saved==="dark"?"dark":"light"; setTheme(initial); document.documentElement.dataset.theme=initial; },[]);
  const toggle=()=>setTheme(old=>{const next=old==="light"?"dark":"light";document.documentElement.dataset.theme=next;localStorage.setItem("noteflow-theme",next);return next;});
  return <ThemeContext.Provider value={{theme,toggle}}>{children}</ThemeContext.Provider>;
}
export const useTheme=()=>useContext(ThemeContext);
