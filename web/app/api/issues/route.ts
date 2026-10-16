import { NextResponse } from "next/server";
import { getIssues, sourceName } from "@/lib/data";

export const dynamic = "force-dynamic";

export async function GET() {
  try {
    return NextResponse.json({ source: sourceName(), issues: await getIssues() });
  } catch (e: any) {
    return NextResponse.json({ error: String(e?.message ?? e) }, { status: 500 });
  }
}
