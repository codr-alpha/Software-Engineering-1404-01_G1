import { useMemo, useState } from "react";
import { useNavigate, useParams, Link } from "react-router-dom";
import { microservices } from "../services/mockMicroservices";

function clamp(n, a, b) {
  return Math.max(a, Math.min(b, n));
}

export default function LessonDetail() {
  const { id } = useParams();
  const navigate = useNavigate();

  const lesson = useMemo(() => {
    const numId = Number(id);
    return microservices.find((x) => x.id === numId) || null;
  }, [id]);


  const initialWords = useMemo(() => {
    const fallback = [
      { en: "Vacation", fa: "تعطیلات" },
      { en: "Sightseeing", fa: "گردشگری" },
      { en: "Departure", fa: "حرکت / عزیمت" },
      { en: "Destination", fa: "مقصد" },
      { en: "Reception", fa: "پذیرش" },
      { en: "Luggage", fa: "چمدان" },
    ];

    const list = (lesson?.wordList && lesson.wordList.length > 0) ? lesson.wordList : fallback;


    return list.map((w) => ({
      id: crypto?.randomUUID ? crypto.randomUUID() : String(Date.now() + Math.random()),
      en: w.en,
      fa: w.fa,
      status: "none", // "know" | "dontknow" | "learned" | "none"

      cells: Array.from({ length: 8 }, () => "empty"), // "green" | "orange" | "empty"
    }));
  }, [lesson]);

  const [rows, setRows] = useState(initialWords);

  if (!lesson) {
    return (
      <div className="t9-page" dir="rtl" lang="fa">
        <header className="t9-topbar">
          <button className="t9-pillBtn" onClick={() => navigate("/microservices")}>
            بازگشت
          </button>
          <h1 className="t9-title">درس پیدا نشد</h1>
          <button className="t9-pillBtn" onClick={() => navigate("/microservices")}>
            خانه
          </button>
        </header>

        <section className="t9-panel">
          <p style={{ color: "var(--navy)" }}>
            این درس وجود ندارد یا هنوز در mock تعریف نشده است.
          </p>
        </section>
      </div>
    );
  }


  const learnedCount = rows.filter((r) => r.status === "learned").length;
  const total = rows.length;
  const progressPct = total === 0 ? 0 : Math.round((learnedCount / total) * 100);

  const mark = (rowId, type) => {
    setRows((prev) =>
      prev.map((r) => {
        if (r.id !== rowId) return r;


        if (r.status === "learned") return r;


        const next = [...r.cells];
        const lastIdx = next.length - 1;

        if (type === "know") next[lastIdx] = "green";
        if (type === "dontknow") next[lastIdx] = "orange";


        const greenCount = next.filter((c) => c === "green").length;
        const learned = greenCount >= clamp(Math.ceil(next.length * 0.75), 4, next.length);

        return {
          ...r,
          status: learned ? "learned" : type,
          cells: next,
        };
      })
    );
  };

  const removeWord = (rowId) => {
    setRows((prev) => prev.filter((r) => r.id !== rowId));
  };

  return (
    <div className="t9-page" dir="rtl" lang="fa">
      <header className="t9-topbar t9-topbar--detail">
        <div className="t9-topbarLeft">
          <button className="t9-pillBtn" onClick={() => navigate("/microservices")}>
            بازگشت
          </button>

            <button
            className="t9-pillBtn"
            onClick={() => navigate(`/microservices/${id}/review`)}
            >
            مرور لغات
            </button>

        </div>

        <h1 className="t9-title">{lesson.title}</h1>
      </header>

      <section className="t9-panel">
        <div className="t9-lessonMeta">
          <div>تعداد کلمات: {total}</div>
          <div>پیشرفت: %{progressPct}</div>
        </div>

        <div className="t9-wordsBox">
          {rows.map((r) => (
            <div className="t9-wordRow" key={r.id}>
              
              <div className="t9-wordEn">{r.en}</div>

              
              <div className="t9-wordActions">
                {r.status === "learned" ? (
                  <span className="t9-learnedTag">یاد گرفته شده</span>
                ) : (
                  <>
                    <button className="t9-chip t9-chip--green" onClick={() => mark(r.id, "know")}>
                      میدانم
                    </button>
                    <button className="t9-chip t9-chip--orange" onClick={() => mark(r.id, "dontknow")}>
                      نمیدانم
                    </button>
                  </>
                )}
              </div>

              
              <div className="t9-cells">
                {r.cells.map((c, i) => (
                  <span
                    key={i}
                    className={[
                      "t9-cell",
                      c === "green" ? "t9-cell--green" : "",
                      c === "orange" ? "t9-cell--orange" : "",
                    ].join(" ")}
                    aria-hidden="true"
                  />
                ))}
              </div>

             
              <button className="t9-trashBtn" onClick={() => removeWord(r.id)} title="حذف واژه">
                🗑️
              </button>
            </div>
          ))}
        </div>


      </section>
    </div>
  );
}
