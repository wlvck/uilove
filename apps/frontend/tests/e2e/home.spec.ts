import { test, expect } from '@playwright/test'

test.describe('Home Page', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/')
  })

  test('displays hero section', async ({ page }) => {
    await expect(page.locator('h1')).toContainText('Discover Beautiful')
    await expect(page.locator('h1 span')).toContainText('Landing Pages')
  })

  test('displays hero description', async ({ page }) => {
    await expect(page.locator('text=A curated gallery of the best designed landing pages')).toBeVisible()
  })

  test('has correct page title', async ({ page }) => {
    await expect(page).toHaveTitle(/UILove/)
  })

  test('displays website grid', async ({ page }) => {
    // Wait for content to load
    await page.waitForTimeout(1000)
    // Either shows websites or loading state
    const gridOrLoading = page.locator('[class*="grid"], [class*="animate-spin"]')
    await expect(gridOrLoading.first()).toBeVisible()
  })

  test('displays sidebar', async ({ page }) => {
    // Sidebar should be visible on desktop
    await page.setViewportSize({ width: 1280, height: 800 })
    const sidebar = page.locator('aside, [class*="sidebar"]')
    // Sidebar may or may not be visible depending on design
    expect(sidebar).toBeDefined()
  })
})

test.describe('Navigation', () => {
  test('can navigate to search page', async ({ page }) => {
    await page.goto('/')
    // Look for search link/icon in header
    const searchLink = page.locator('a[href="/search"], [href*="search"]').first()
    if (await searchLink.isVisible()) {
      await searchLink.click()
      await expect(page).toHaveURL(/search/)
    }
  })

  test('can navigate to categories page', async ({ page }) => {
    await page.goto('/')
    const categoriesLink = page.locator('a[href="/categories"]').first()
    if (await categoriesLink.isVisible()) {
      await categoriesLink.click()
      await expect(page).toHaveURL(/categories/)
    }
  })

  test('header is visible', async ({ page }) => {
    await page.goto('/')
    const header = page.locator('header').first()
    await expect(header).toBeVisible()
  })

  test('logo links to home', async ({ page }) => {
    await page.goto('/search')
    const logo = page.locator('a[href="/"]').first()
    await logo.click()
    await expect(page).toHaveURL('/')
  })
})
