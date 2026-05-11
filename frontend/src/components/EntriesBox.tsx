

export interface Entry {
  date: string;
  internship_id: number;
  description: string;
  hours: number;
  skill_ids: string[];
  links: string;
  mood_slider: number;
  blockers: string;
  learnings: string;
}

interface Props {
  entries: Entry[];
}

function EntriesBox({ entries }: Props) {
  return (
    <div className="entries-box">
      <h2>Generated Entries</h2>

      {entries.length === 0 ? (
        <p>No entries generated yet.</p>
      ) : (
        <div className="entries-container">
          {entries.map((entry, index) => (
            <div className="entry-card" key={index}>
              
              {/* Header */}
              <div className="entry-header">
                <h3>{entry.date}</h3>
                <span className="entry-hours">{entry.hours} hrs</span>
              </div>

              {/* Meta Info */}
              <div className="entry-meta">
                <p><strong>Internship ID:</strong> {entry.internship_id}</p>
                <p><strong>Mood:</strong> {entry.mood_slider}/10</p>
              </div>

              {/* Description */}
              <div className="entry-section scroll-box">
                <strong>Description</strong>
                <p>{entry.description}</p>
              </div>

              {/* Skills */}
              <div className="entry-section scroll-box">
                <strong>Skills</strong>
                <p>
                  {entry.skill_ids.length
                    ? entry.skill_ids.join(", ")
                    : "None"}
                </p>
              </div>

              {/* Blockers */}
              <div className="entry-section scroll-box">
                <strong>Blockers</strong>
                <p>{entry.blockers || "None"}</p>
              </div>

              {/* Learnings */}
              <div className="entry-section scroll-box">
                <strong>Learnings</strong>
                <p>{entry.learnings || "None"}</p>
              </div>

              {/* Links */}
              <div className="entry-section">
                <strong>Links</strong>
                <p>
                  {entry.links ? (
                    <a href={entry.links} target="_blank" rel="noreferrer">
                      {entry.links}
                    </a>
                  ) : (
                    "None"
                  )}
                </p>
              </div>

            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default EntriesBox;