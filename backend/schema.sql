-- Fact Checker Database Schema for Supabase

-- Create the fact_checks table
CREATE TABLE IF NOT EXISTS fact_checks (
  id BIGSERIAL PRIMARY KEY,
  claim TEXT NOT NULL,
  verdict TEXT NOT NULL,
  explanation TEXT,
  sources TEXT[],
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create an index on created_at for faster queries
CREATE INDEX IF NOT EXISTS idx_fact_checks_created_at ON fact_checks(created_at DESC);

-- Enable Row Level Security (RLS)
ALTER TABLE fact_checks ENABLE ROW LEVEL SECURITY;

-- Create a policy that allows all operations (for simplicity)
-- In production, you'd want more restrictive policies
CREATE POLICY "Allow all operations" ON fact_checks
  FOR ALL
  USING (true)
  WITH CHECK (true);