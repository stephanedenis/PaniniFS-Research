// sign-runtime.spec.js
// Minimal stub: ensures modules load (skips if fetch blocked under file://)
import { test, expect } from '@playwright/test';

// Assuming a static server will serve tech/apps/demos
const DEMO_PATH = 'tech/apps/demos/universal_sign_interface.html';

function runningInFileProtocol(){
  return process.env.PW_BASE_URL ? false : true;
}

test.describe('sign runtime', () => {
  test('can access signRuntime after load', async ({ page }) => {
    test.skip(runningInFileProtocol(), 'Skipping under file:// environment');
    await page.goto(DEMO_PATH);
    await page.waitForFunction(() => window.signRuntime && window.signRuntime.data);
    const versions = await page.evaluate(() => ({
      hand: window.signRuntime.data.getHandshapes().length,
      facial: window.signRuntime.data.getFacialPresets().length
    }));
    expect(versions.hand).toBeGreaterThan(0);
    expect(versions.facial).toBeGreaterThan(0);
  });
});
