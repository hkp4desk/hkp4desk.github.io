export type Locale = "zh" | "en";
export const LOCALES: Locale[] = ["zh", "en"];

export const site = {
  name: "HKP4",
  url: "https://hkp4.github.io",
  patreon: "https://www.patreon.com/c/hkp4",
  email: "hkp4-desk@proton.me",
  title: {
    zh: "HKP4 · 香港的四個面向",
    en: "HKP4 · Four Lenses on Hong Kong",
  },
  tagline: {
    zh: "繁榮 Prosperity · 推演 Projection · 前景 Prospect · 潛能 Potential —— 一份匿名的香港觀察刊物",
    en: "Prosperity · Projection · Prospect · Potential — an anonymous journal on Hong Kong",
  },
  author: {
    zh: "HKP4 編輯部",
    en: "The HKP4 Desk",
  },
};

export const ui = {
  zh: {
    nav_home: "首頁",
    nav_articles: "文章",
    nav_about: "關於",
    nav_donate: "打賞",
    support: "在 Patreon 支持我們",
    support_short: "支持我們",
    latest: "最新文章",
    all_articles: "全部文章",
    read_more: "繼續閱讀",
    back: "← 返回文章列表",
    empty: "這裡還沒有文章。",
    also_lang: "本文另有英文版本 English version →",
    translated_from: "本文自繁中譯出 Translated from Chinese",
    no_lang: "此篇暫無英文版本",
    why_anonymous: "我們為什麼匿名",
    patreon_pitch_title: "如果這篇文章對你有幫助",
    patreon_pitch_body:
      "HKP4 由匿名的個人作者以業餘時間寫作,沒有機構資助。你的每月支持,是這個刊物存在下去的唯一理由。",
    donate_more: "其他支持方式(加密貨幣)→",
    footer_about: "關於本刊",
    footer_follow: "訂閱與鏈接",
    rss: "訂閱 RSS",
    rights: "本站文章可自由轉載,請註明出處並保持全文完整。",
    lang_label: "English",
    p_label: "面向",
  },
  en: {
    nav_home: "Home",
    nav_articles: "Articles",
    nav_about: "About",
    nav_donate: "Donate",
    support: "Support us on Patreon",
    support_short: "Support",
    latest: "Latest Articles",
    all_articles: "All Articles",
    read_more: "Read more",
    back: "← All articles",
    empty: "No articles yet.",
    also_lang: "中文版本 Chinese version →",
    translated_from: "Translated from Chinese 自繁中譯出",
    no_lang: "Not yet available in Chinese",
    why_anonymous: "Why we are anonymous",
    patreon_pitch_title: "Found this useful?",
    patreon_pitch_body:
      "HKP4 is written in spare time by an anonymous individual, with no institutional funding. Your monthly support is the only reason this journal exists.",
    donate_more: "Other ways to support (crypto) →",
    footer_about: "About",
    footer_follow: "Subscribe & links",
    rss: "RSS feed",
    rights: "Articles may be freely reposted with attribution and full text intact.",
    lang_label: "繁中",
    p_label: "Lens",
  },
} as const;

export type UIKey = keyof (typeof ui)["zh"];

export type PKey = "prosperity" | "projection" | "prospect" | "potential";

export const P_ORDER: PKey[] = ["prosperity", "projection", "prospect", "potential"];

export const PS: Record<
  PKey,
  { zh: string; en: string; desc: { zh: string; en: string } }
> = {
  prosperity: {
    zh: "繁榮",
    en: "Prosperity",
    desc: {
      zh: "經濟、樓市、就業與民生:錢從哪裡來,往哪裡去。",
      en: "Economy, property, jobs and livelihood: where the money comes from and where it goes.",
    },
  },
  projection: {
    zh: "推演",
    en: "Projection",
    desc: {
      zh: "以現有數據與制度軌跡,對香港三五年內的情景做誠實的推演。",
      en: "Honest scenario projections for Hong Kong's next three to five years, extrapolated from data and institutional trajectories.",
    },
  },
  prospect: {
    zh: "前景",
    en: "Prospect",
    desc: {
      zh: "政策走向、制度演化與區域競合:香港下一個機會窗口在哪裡。",
      en: "Policy direction, institutional evolution and regional competition: where Hong Kong's next window of opportunity opens.",
    },
  },
  potential: {
    zh: "潛能",
    en: "Potential",
    desc: {
      zh: "尚未被釋放的能力:人才、資本、法治與東西門戶的剩餘紅利。",
      en: "Unreleased capacity: the remaining dividends of talent, capital, rule of law and Hong Kong's gatekeeper role between East and West.",
    },
  },
};

/** 把无语言前缀的路径映射到指定语言 */
export function localize(locale: Locale, path: string): string {
  const clean = path.replace(/^\/en(\/|$)/, "$1") || "/";
  const normalized = clean === "" ? "/" : clean;
  if (locale === "en") return normalized === "/" ? "/en/" : "/en" + normalized;
  return normalized;
}

export function otherLocale(locale: Locale): Locale {
  return locale === "zh" ? "en" : "zh";
}

export function fmtDate(d: Date, locale: Locale): string {
  return d.toLocaleDateString(locale === "zh" ? "zh-Hant-HK" : "en-GB", {
    year: "numeric",
    month: "long",
    day: "numeric",
    timeZone: "UTC",
  });
}
