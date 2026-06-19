#!/usr/bin/env node
const keyId = process.env.RAZORPAY_KEY_ID;
const keySecret = process.env.RAZORPAY_KEY_SECRET;
if (!keyId || !keySecret) {
  console.error('RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET are required for sandbox verification.');
  process.exit(2);
}
async function main() {
  const auth = Buffer.from(`${keyId}:${keySecret}`).toString('base64');
  const create = await fetch('https://api.razorpay.com/v1/orders', {
    method: 'POST',
    headers: { authorization: `Basic ${auth}`, 'content-type': 'application/json' },
    body: JSON.stringify({ amount: 100, currency: 'INR', receipt: `fitforge_sandbox_${Date.now()}` }),
  });
  const order = await create.json();
  if (!create.ok) throw new Error(`Create order failed: ${JSON.stringify(order)}`);
  const fetchOrder = await fetch(`https://api.razorpay.com/v1/orders/${order.id}`, { headers: { authorization: `Basic ${auth}` } });
  const fetched = await fetchOrder.json();
  if (!fetchOrder.ok) throw new Error(`Fetch order failed: ${JSON.stringify(fetched)}`);
  console.log(JSON.stringify({ ok: true, orderId: fetched.id, status: fetched.status }, null, 2));
}
main().catch((error) => { console.error(error); process.exit(1); });
