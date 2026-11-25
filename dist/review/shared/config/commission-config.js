export const config = {
 programName:'Moonshine Capital Broker Commission Calculator',version:'1.0.0-demo',effectiveDate:null,verificationStatus:'demonstration',approvedSource:null,currency:'USD',
 limits:{deals:1000,amount:10000000,rate:100,growth:25,expense:10000000,target:100000000},
 products:[['business','Business Capital'],['revenue','Revenue-Based Funding'],['asset','Asset-Backed Funding'],['commerce','SaaS / E-commerce Funding'],['credit','Business Credit']].map(([id,name])=>({id,name,method:'percentage',rate:3,basis:'funded_amount',eligible:true})),
 tiers:[{name:'Pre-production',min:0,max:0},{name:'Bronze',min:1,max:10},{name:'Silver',min:11,max:25},{name:'Gold',min:26,max:50},{name:'Platinum',min:51,max:null}],
 bonuses:[],recurring:[],paymentDelay:0,deductions:[],clawbacks:[],features:{bonuses:false,recurring:false,teamOverrides:false},
 scenarios:[{id:'conservative',name:'Conservative',factor:.6},{id:'base',name:'Base Case',factor:1},{id:'optimistic',name:'Optimistic',factor:1.4}]
};
export const disclosure='Hypothetical gross commission estimates. Actual earnings vary and are not guaranteed.';
export const methodology='Estimates depend on funded transactions, eligible products, compensation agreements, payment timing, business expenses, cancellations, clawbacks, individual performance and selected assumptions. Gross commissions are not salary, take-home pay or net business income. Consult the applicable partner agreement for official compensation terms. Scenario factors are illustrative planning assumptions, not statistical predictions. Fractional deals in projections represent expected production, not actual transactions.';
export function defaultState(c=config){return {deals:10,amount:50000,allocation:Object.fromEntries(c.products.filter(p=>p.eligible).map(p=>[p.id,100/c.products.filter(p=>p.eligible).length])),rates:Object.fromEntries(c.products.map(p=>[p.id,(p.method==='fixed'?p.fixed:p.rate)??0])),scenario:'base',factors:{conservative:.6,base:1,optimistic:1.4},growth:0,ramp:0,capacity:1000,retention:100,delay:0,expense:0,target:15000,horizon:36,bonuses:false,recurring:false};}
