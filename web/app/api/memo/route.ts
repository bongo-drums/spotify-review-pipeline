import { NextResponse } from "next/server";
import { getClaims, getMemo, sourceName } from "@/lib/data";

export const dynamic = "force-dynamic";

export async function GET() {
  try {
    const [memo, claims] = await Promise.all([getMemo(), getClaims()]);
    return NextResponse.json({ source: sourceName(), memo, claims });
  } catch (e: any) {
    return NextResponse.json({ error: String(e?.message ?? e) }, { status: 500 });
  }
}
