import { NextResponse } from "next/server";
import { getAggregates, getRun, sourceName } from "@/lib/data";

export const dynamic = "force-dynamic";

export async function GET() {
  try {
    const [run, aggregates] = await Promise.all([getRun(), getAggregates()]);
    return NextResponse.json({ source: sourceName(), run, aggregates });
  } catch (e: any) {
    return NextResponse.json({ error: String(e?.message ?? e) }, { status: 500 });
  }
}
