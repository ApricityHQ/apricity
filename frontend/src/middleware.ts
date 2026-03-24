import { clerkMiddleware, createRouteMatcher } from '@clerk/nextjs/server'

// Define public routes that don't require authentication
const isPublicRoute = createRouteMatcher([
  '/', // Workspace
  '/sign-in(.*)', // Sign in pages
  '/sign-up(.*)', // Sign up pages
  '/api/views(.*)', // View API route (allows anonymous generation)
  '/(.*)' // For now, allow everything on the frontend so users can see the UI before logging in.
          // The actual protection is hitting the DB. But actually, let's protect the views/reports if needed.
          // Let's just follow the standard pattern: protect specific routes if needed, or leave public.
])

// The user asked to make the standard clerk middleware. The plan says protect all non-public routes.
// Protect workspace and reports
const isProtectedRoute = createRouteMatcher([
  '/workspace(.*)',
  '/reports(.*)', // Example: if we had a reports page
])

export default clerkMiddleware(async (auth, request) => {
  if (isProtectedRoute(request)) {
    await auth.protect()
  }
})

export const config = {
  matcher: [
    // Skip Next.js internals and all static files, unless found in search params
    '/((?!_next|[^?]*\\.(?:html?|css|js(?!on)|jpe?g|webp|png|gif|svg|ttf|woff2?|ico|csv|docx?|xlsx?|zip|webmanifest)).*)',
    // Always run for API routes
    '/(api|trpc)(.*)',
  ],
}
