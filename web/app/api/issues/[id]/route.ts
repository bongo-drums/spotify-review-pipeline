import { NextResponse } from "next/server";
import { getIssue, sourceName } from "@/lib/data";

export const dynamic = "force-dynamic";

export async function GET(_req: Request, ctx: { params: Promise<{ id: string }> }) {
  try {
    const { id } = await ctx.params;
    const detail = await getIssue(decodeURIComponent(id));
    if (!detail) return NextResponse.json({ error: "unknown issue" }, { status: 404 });
    return NextResponse.json({ source: sourceName(), ...detail });
  } catch (e: any) {
    return NextResponse.json({ error: String(e?.message ?? e) }, { status: 500 });
  }
}
