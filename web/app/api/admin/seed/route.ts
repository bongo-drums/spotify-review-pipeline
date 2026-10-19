import { NextResponse } from "next/server";
import { getPool, sourceName } from "@/lib/data";
import { seedFromSnapshot } from "@/lib/seed";

export const dynamic = "force-dynamic";
export const maxDuration = 60;

/** Load (or with ?force=1 reload) the committed web/data snapshot into the database the app is configured for. */
export async function GET(req: Request) {
  if (sourceName() !== "postgres") return NextResponse.json({ error: "no DATABASE_URL; the app is serving web/data directly" }, { status: 400 });
  try {
    const force = new URL(req.url).searchParams.get("force") === "1";
    const result = await seedFromSnapshot(await getPool(), force);
    return NextResponse.json({ source: sourceName(), ...result });
  } catch (e: any) {
    return NextResponse.json({ error: String(e?.message ?? e) }, { status: 500 });
  }
}
