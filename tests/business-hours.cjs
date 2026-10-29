/* Calendar-only regression; no network, DOM or customer data. */
const assert=require('node:assert/strict');
const hours=require('../assets/business-hours.js');
let months=0,dates=0;
for(let year=2000;year<=2100;year++)for(let month=1;month<=12;month++){
 const value=hours.lastSaturday(year,month),date=new Date(value+'T12:00:00Z');assert.equal(date.getUTCFullYear(),year);assert.equal(date.getUTCMonth()+1,month);assert.equal(date.getUTCDay(),6);assert.equal(hours.availability(value).kind,'umuganda');assert.equal(hours.availability(value).opens,'12:00');assert.equal(hours.availability(value).appointmentRequired,true);
 const next=new Date(date);next.setUTCDate(next.getUTCDate()+7);assert.notEqual(next.getUTCMonth()+1,month);
 for(let day=1;day<=new Date(Date.UTC(year,month,0)).getUTCDate();day++){const iso=`${year}-${String(month).padStart(2,'0')}-${String(day).padStart(2,'0')}`,d=new Date(iso+'T12:00:00Z'),a=hours.availability(iso);if(d.getUTCDay()===0){assert.equal(a.kind,'sunday');assert.equal(a.opens,null);assert.equal(a.closes,null);assert.equal(a.appointmentRequired,true)}else if(d.getUTCDay()===6&&iso!==value){assert.equal(a.kind,'saturday');assert.equal(a.opens,'09:00');assert.equal(a.closes,'17:00');assert.equal(a.appointmentRequired,false)}dates++}months++;
 assert(!hours.timeAllowed(value,'09:00 AM - 10:00 AM'));assert(!hours.timeAllowed(value,'11:00 AM - 12:00 PM'));assert(hours.timeAllowed(value,'12:00 PM - 01:00 PM'));assert(hours.timeAllowed(value,'04:00 PM - 05:00 PM'));assert(!hours.timeAllowed(value,'05:00 PM - 06:00 PM'));
}
for(const invalid of ['','2026-02-30','2026-13-01','29/10/2026','not-a-date'])assert.equal(hours.availability(invalid),null);
assert.equal(hours.lastSaturday(2026,10),'2026-10-31'); // fifth Saturday, not the fourth
assert.equal(hours.lastSaturday(2027,2),'2027-02-27');
console.log(`PASS: ${months} months / ${dates} calendar dates (2000–2100), leap/century and fifth-Saturday cases; Umuganda noon–5, ordinary Saturday walk-ins, Sunday without invented hours.`);
