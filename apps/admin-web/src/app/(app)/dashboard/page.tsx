import { Card } from '@/components/ui';
const metrics = ['Active Members','Today Attendance','Renewal Revenue','Product Sales','PT Bookings','WhatsApp Sent'];
export default function Dashboard(){ return <section className='space-y-6 p-8'><h2 className='text-5xl font-black'>Production Dashboard</h2><div className='grid gap-4 md:grid-cols-3'>{metrics.map((m,i)=><Card key={m}><p className='text-zinc-400'>{m}</p><strong className='text-3xl text-yellow-400'>{[3842,642,'INR 8.2L','INR 2.4L',91,1280][i]}</strong></Card>)}</div></section> }
