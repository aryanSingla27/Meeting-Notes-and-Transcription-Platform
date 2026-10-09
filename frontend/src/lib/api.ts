export const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";

export type Participant = { id?: number; name: string; email?: string | null };
export type Transcript = { id: number; speaker: string; start_time: number; end_time: number; text: string };
export type ActionItem = { id: number; title: string; description: string; assignee: string; completed: boolean };
export type Summary = { id: number; overview: string; key_topics: string[]; outline: string[] };
export type Meeting = { id: number; title: string; date: string; duration: number; created_at: string; updated_at: string; participants: Participant[]; transcript: Transcript[]; summary?: Summary | null; action_items: ActionItem[] };

async function request<T>(path:string, options?:RequestInit):Promise<T>{
  const res=await fetch(`${API}${path}`,{...options,headers:{"Content-Type":"application/json",...(options?.headers||{})},cache:"no-store"});
  if(!res.ok){const msg=await res.text(); throw new Error(msg || `Request failed (${res.status})`)}
  if(res.status===204) return undefined as T;
  return res.json();
}
export const api={
  meetings:(params="")=>request<Meeting[]>(`/meetings${params}`),
  meeting:(id:number)=>request<Meeting>(`/meetings/${id}`),
  create:(body:unknown)=>request<Meeting>("/meetings",{method:"POST",body:JSON.stringify(body)}),
  update:(id:number,body:unknown)=>request<Meeting>(`/meetings/${id}`,{method:"PUT",body:JSON.stringify(body)}),
  remove:(id:number)=>request<void>(`/meetings/${id}`,{method:"DELETE"}),
  addAction:(id:number,body:unknown)=>request<ActionItem>(`/meetings/${id}/actions`,{method:"POST",body:JSON.stringify(body)}),
  updateAction:(id:number,body:unknown)=>request<ActionItem>(`/actions/${id}`,{method:"PUT",body:JSON.stringify(body)}),
  deleteAction:(id:number)=>request<void>(`/actions/${id}`,{method:"DELETE"}),
  updateSummary:(id:number,body:unknown)=>request<Summary>(`/meetings/${id}/summary`,{method:"PUT",body:JSON.stringify(body)})
};
