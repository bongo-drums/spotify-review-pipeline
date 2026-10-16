import { NextResponse } from "next/server";
import { getReview, sourceName } from "@/lib/data";

export const dynamic = "force-dynamic";

export async function GET(_req: Request, ctx: { params: Promise<{ id: string }> }) {
  try {
    const { id } = await ctx.params;
    const review = await getReview(decodeURIComponent(id));
    if (!review) return NextResponse.json({ error: "unknown review" }, { status: 404 });
    return NextResponse.json({ source: sourceName(), review });
  } catch (e: any) {
    return NextResponse.json({ error: String(e?.message ?? e) }, { status: 500 });
  }
}
