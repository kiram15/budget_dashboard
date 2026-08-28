// Maps Transaction.display_category -> one of four buckets for the
// Breakdown page. This is the single place that rule lives — once this is
// wired to real data, this is almost certainly a field the user sets when
// managing their own Category list (see project notes: Category is
// user-owned, separate from Plaid's auto-categorization), not something
// inferred automatically. A `bucket` field on the Category model would let
// this mapping move server-side; until then, this file is the seam.

export const BUCKETS = {
  unavoidable: { label: 'Unavoidable', color: 'ink' },
  fun: { label: 'Fun', color: 'discretionary' },
  investments: { label: 'Investments', color: 'accent' },
}

export const CATEGORY_BUCKET = {
  Housing: 'unavoidable',
  Groceries: 'unavoidable',
  Utilities: 'unavoidable',
  Insurance: 'unavoidable',
  Transport: 'unavoidable',
  Subscriptions: 'fun',
  Shopping: 'fun',
  'Dining Out': 'fun',
  Entertainment: 'fun',
  'Investment Contributions': 'investments',
}

export function bucketFor(category) {
  return CATEGORY_BUCKET[category] || 'fun'
}
