"use client";
import { X } from "lucide-react";
export function Modal({title,onClose,children,footer}:{title:string;onClose:()=>void;children:React.ReactNode;footer?:React.ReactNode}){return <div className="modal-backdrop" onMouseDown={e=>{if(e.target===e.currentTarget)onClose()}}><div className="modal"><div className="modal-head"><h3>{title}</h3><button className="icon-btn" onClick={onClose}><X size={15}/></button></div><div className="modal-body">{children}</div>{footer&&<div className="modal-footer">{footer}</div>}</div></div>}
