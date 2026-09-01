import { driver } from 'driver.js'
import type { DriveStep } from 'driver.js'
import 'driver.js/dist/driver.css'
import { useI18n } from 'vue-i18n'
import { useAuth } from '@/features/auth/composables/useAuth'
import { api } from '@/lib/api'

export function useOnboardingTour() {
  const { t } = useI18n()
  const { user, me } = useAuth()

  function isMobileViewport(): boolean {
    return typeof window !== 'undefined' && window.innerWidth < 768
  }

  function isTourCompleted(): boolean {
    return user.value?.settings?.onboarding?.tourCompleted === true
  }

  function buildSteps(): DriveStep[] {
    const candidates: DriveStep[] = [
      // Left sidebar - top to bottom
      {
        element: '[data-tour="sidebar-libraries"]',
        popover: {
          title: t('onboarding.steps.libraries.title'),
          description: t('onboarding.steps.libraries.description'),
          side: 'right',
          align: 'start',
          showButtons: ['next', 'close'],
        },
      },
      {
        element: '[data-tour="sidebar-smartScopes"]',
        popover: {
          title: t('onboarding.steps.smartScopes.title'),
          description: t('onboarding.steps.smartScopes.description'),
          side: 'right',
          align: 'start',
        },
      },
      {
        element: '[data-tour="sidebar-collections"]',
        popover: {
          title: t('onboarding.steps.collections.title'),
          description: t('onboarding.steps.collections.description'),
          side: 'right',
          align: 'start',
        },
      },
      // Header - left to right
      {
        element: '[data-tour="global-search"]',
        popover: {
          title: t('onboarding.steps.globalSearch.title'),
          description: t('onboarding.steps.globalSearch.description'),
          side: 'bottom',
          align: 'start',
        },
      },
      {
        element: '[data-tour="book-dock-btn"]',
        popover: {
          title: t('onboarding.steps.bookDock.title'),
          description: t('onboarding.steps.bookDock.description'),
          side: 'bottom',
          align: 'end',
        },
      },
      {
        element: '[data-tour="statistics-btn"]',
        popover: {
          title: t('onboarding.steps.statistics.title'),
          description: t('onboarding.steps.statistics.description'),
          side: 'bottom',
          align: 'end',
        },
      },
      {
        element: '[data-tour="upload-button"]',
        popover: {
          title: t('onboarding.steps.upload.title'),
          description: t('onboarding.steps.upload.description'),
          side: 'bottom',
          align: 'end',
        },
      },
      {
        element: '[data-tour="appearance-picker"]',
        popover: {
          title: t('onboarding.steps.appearance.title'),
          description: t('onboarding.steps.appearance.description'),
          side: 'bottom',
          align: 'end',
        },
      },
    ]

    return candidates.filter((step) => document.querySelector(step.element as string) !== null)
  }

  function markCompletedLocally(): void {
    if (!user.value) return
    user.value = {
      ...user.value,
      settings: {
        ...user.value.settings,
        onboarding: { tourCompleted: true },
      },
    }
  }

  function persistCompletion(): void {
    api('/api/v1/users/me/settings', {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ settings: { onboarding: { tourCompleted: true } } }),
    }).catch(() => {})
  }

  function startTour(): void {
    const steps = buildSteps()
    if (steps.length === 0) return

    const driverObj = driver({
      showProgress: true,
      progressText: t('onboarding.progressText', { current: '{{current}}', total: '{{total}}' }),
      nextBtnText: t('onboarding.next'),
      prevBtnText: t('onboarding.back'),
      doneBtnText: t('onboarding.done'),
      disableActiveInteraction: true,
      onDestroyed: () => {
        markCompletedLocally()
        persistCompletion()
      },
      steps,
    })

    driverObj.drive()
  }

  function maybeStartTour(): void {
    if (isMobileViewport()) return
    if (isTourCompleted()) return
    startTour()
  }

  async function resetTour(): Promise<void> {
    await api('/api/v1/users/me/settings', {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ settings: { onboarding: { tourCompleted: false } } }),
    })
    await me()
    startTour()
  }

  return { maybeStartTour, startTour, resetTour }
}
