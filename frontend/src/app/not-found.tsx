import Link from "next/link";
export default function NotFound(){return <div className="empty" style={{marginTop:100}}><h2>Page not found</h2><p>That page does not exist.</p><Link href="/" className="primary" style={{display:"inline-flex",textDecoration:"none",marginTop:12}}>Back to meetings</Link></div>}
