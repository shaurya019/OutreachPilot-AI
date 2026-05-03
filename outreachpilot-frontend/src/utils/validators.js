import { z } from "zod";

export const researchFormSchema = z.object({
  company_name: z
    .string()
    .min(2, "Company name is required"),

  company_website: z
    .string()
    .url("Enter a valid company website URL"),

  company_linkedin: z
    .string()
    .optional()
    .or(z.literal("")),

  employee_name: z
    .string()
    .min(2, "Employee name is required"),

  employee_linkedin: z
    .string()
    .optional()
    .or(z.literal("")),

  employee_email: z
    .string()
    .email("Enter a valid employee email")
    .optional()
    .or(z.literal("")),

  employee_profile_text: z
    .string()
    .optional()
    .or(z.literal("")),

  user_email: z
    .string()
    .email("Enter a valid user email"),

  user_profile: z
    .string()
    .min(20, "Please provide at least 20 characters about your profile"),

  purpose: z.enum(["job_outreach", "interview_prep", "sales_outreach"]),
});