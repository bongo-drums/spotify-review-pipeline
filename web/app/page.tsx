import Dashboard from "@/components/Dashboard";

export default function Page() {
  return (
    <main>
      <h1>Spotify review insights</h1>
      <p className="lede">
        Every number on this page is read by the backend from the pipeline database and served through <code>/api/*</code>.
        Issue rankings are the reproducible baseline (priority score = complaint count × mean severity); the recommendation
        was generated once from those saved aggregates and every figure in it carries a claim ID.
      </p>
      <Dashboard />
      <footer>
        Source: Spotify Google Play reviews, 2022-05-17 to 2023-11-15 (course extract). Labels: <code>claude-haiku-5-5</code>,
        label set <code>labels-v1</code>. Reviews are self-selected public text; counts are complaints, not users.
      </footer>
    </main>
  );
}
